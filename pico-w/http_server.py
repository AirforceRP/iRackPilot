"""
HTTP Server for iRackPilot Pico W
Handles all HTTP API endpoints
"""

import socket
import json
import time
import uasyncio as asyncio

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.ipmi_client = None
        self.script_engine = None
        self.get_status = None
        self.console_active = False
        
    def setup_routes(self, ipmi_client, script_engine, get_status_func):
        """Setup route handlers"""
        self.ipmi_client = ipmi_client
        self.script_engine = script_engine
        self.get_status = get_status_func
    
    async def start(self):
        """Start the HTTP server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        
        print(f"HTTP server listening on {self.host}:{self.port}")
        
        while True:
            try:
                client, addr = self.socket.accept()
                asyncio.create_task(self.handle_client(client, addr))
            except OSError:
                await asyncio.sleep(0.1)
    
    async def handle_client(self, client, addr):
        """Handle incoming client connection"""
        try:
            client.setblocking(False)
            request = await self.read_request(client)
            
            if request:
                response = await self.handle_request(request)
                await self.send_response(client, response)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            try:
                client.close()
            except:
                pass
    
    async def read_request(self, client):
        """Read HTTP request from client"""
        request = b""
        timeout = 5
        start_time = time.ticks_ms()
        
        while True:
            try:
                chunk = client.recv(1024)
                if chunk:
                    request += chunk
                    if b"\r\n\r\n" in request:
                        break
                elif time.ticks_diff(time.ticks_ms(), start_time) > timeout * 1000:
                    break
                await asyncio.sleep(0.01)
            except OSError:
                await asyncio.sleep(0.01)
        
        return request.decode('utf-8', errors='ignore') if request else None
    
    async def handle_request(self, request):
        """Handle HTTP request and return response"""
        try:
            lines = request.split('\r\n')
            if not lines:
                return self.error_response(400, "Bad Request")
            
            method_line = lines[0]
            parts = method_line.split()
            if len(parts) < 2:
                return self.error_response(400, "Bad Request")
            
            method = parts[0]
            path = parts[1].split('?')[0]
            
            # Parse headers
            headers = {}
            body = ""
            body_start = request.find('\r\n\r\n')
            if body_start != -1:
                body = request[body_start + 4:]
            
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            
            # Route handling
            if method == "GET":
                return await self.handle_get(path, headers)
            elif method == "POST":
                return await self.handle_post(path, headers, body)
            else:
                return self.error_response(405, "Method Not Allowed")
                
        except Exception as e:
            print(f"Error handling request: {e}")
            return self.error_response(500, "Internal Server Error")
    
    async def handle_get(self, path, headers):
        """Handle GET requests"""
        if path == "/status":
            status = self.get_status()
            return self.json_response(status)
        
        elif path == "/ipmi/info":
            if self.ipmi_client and self.ipmi_client.is_connected():
                info = self.ipmi_client.get_server_info()
                return self.json_response(info)
            else:
                return self.error_response(503, "Not connected to IPMI server")
        
        elif path == "/ipmi/console/frame":
            if self.console_active and self.ipmi_client:
                frame_data = self.ipmi_client.get_console_frame()
                if frame_data:
                    return self.image_response(frame_data)
                else:
                    return self.error_response(503, "No console frame available")
            else:
                return self.error_response(503, "Console not active")
        
        else:
            return self.error_response(404, "Not Found")
    
    async def handle_post(self, path, headers, body):
        """Handle POST requests"""
        try:
            if body:
                data = json.loads(body)
            else:
                data = {}
        except:
            data = {}
        
        if path == "/ipmi/connect":
            return await self.handle_ipmi_connect(data)
        
        elif path == "/ipmi/disconnect":
            return await self.handle_ipmi_disconnect()
        
        elif path == "/ipmi/console/start":
            return await self.handle_console_start()
        
        elif path == "/ipmi/console/stop":
            return await self.handle_console_stop()
        
        elif path == "/ipmi/console/key":
            return await self.handle_console_key(data)
        
        elif path == "/ipmi/command":
            return await self.handle_ipmi_command(data)
        
        elif path == "/scripts/execute":
            return await self.handle_script_execute(data)
        
        else:
            return self.error_response(404, "Not Found")
    
    async def handle_ipmi_connect(self, data):
        """Handle IPMI connection request"""
        try:
            host = data.get("host")
            port = data.get("port", 623)
            username = data.get("username")
            password = data.get("password")
            vendor = data.get("vendor", "Generic")
            
            if not all([host, username, password]):
                return self.error_response(400, "Missing required parameters")
            
            success = await self.ipmi_client.connect(host, port, username, password, vendor)
            
            if success:
                return self.json_response({"success": True})
            else:
                return self.json_response({"success": False, "error": "Connection failed"})
        except Exception as e:
            return self.json_response({"success": False, "error": str(e)})
    
    async def handle_ipmi_disconnect(self):
        """Handle IPMI disconnection"""
        if self.ipmi_client:
            self.ipmi_client.disconnect()
        return self.json_response({"success": True})
    
    async def handle_console_start(self):
        """Start console session"""
        if self.ipmi_client and self.ipmi_client.is_connected():
            self.console_active = True
            self.ipmi_client.start_console()
            return self.json_response({"success": True})
        else:
            return self.error_response(503, "Not connected to IPMI server")
    
    async def handle_console_stop(self):
        """Stop console session"""
        self.console_active = False
        if self.ipmi_client:
            self.ipmi_client.stop_console()
        return self.json_response({"success": True})
    
    async def handle_console_key(self, data):
        """Handle keyboard input"""
        key = data.get("key", "")
        if self.ipmi_client and self.console_active:
            self.ipmi_client.send_key(key)
            return self.json_response({"success": True})
        else:
            return self.error_response(503, "Console not active")
    
    async def handle_ipmi_command(self, data):
        """Execute IPMI command"""
        command = data.get("command", "")
        if not command:
            return self.error_response(400, "Command required")
        
        if self.ipmi_client and self.ipmi_client.is_connected():
            result = await self.ipmi_client.execute_command(command)
            return self.json_response({"success": True, "output": result})
        else:
            return self.error_response(503, "Not connected to IPMI server")
    
    async def handle_script_execute(self, data):
        """Execute script"""
        language = data.get("language", "")
        content = data.get("content", "")
        
        if not language or not content:
            return self.error_response(400, "Language and content required")
        
        try:
            result = await self.script_engine.execute(language, content)
            return self.json_response({
                "success": True,
                "output": result
            })
        except Exception as e:
            return self.json_response({
                "success": False,
                "error": str(e)
            })
    
    def json_response(self, data, status_code=200):
        """Create JSON response"""
        json_str = json.dumps(data)
        status_text = "OK" if status_code == 200 else "Error"
        
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        response += "Content-Type: application/json\r\n"
        response += f"Content-Length: {len(json_str)}\r\n"
        response += "Access-Control-Allow-Origin: *\r\n"
        response += "\r\n"
        response += json_str
        
        return response.encode()
    
    def image_response(self, image_data):
        """Create image response"""
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: image/jpeg\r\n"
        response += f"Content-Length: {len(image_data)}\r\n"
        response += "\r\n"
        
        return response.encode() + image_data
    
    def error_response(self, status_code, message):
        """Create error response"""
        error_data = {"success": False, "error": message}
        return self.json_response(error_data, status_code)
    
    async def send_response(self, client, response):
        """Send HTTP response to client"""
        try:
            if isinstance(response, bytes):
                await asyncio.sleep(0)
                client.sendall(response)
            else:
                client.sendall(response.encode())
        except Exception as e:
            print(f"Error sending response: {e}")

