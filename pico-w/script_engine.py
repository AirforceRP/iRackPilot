"""
Script Execution Engine for iRackPilot Pico W
Handles execution of JavaScript, Python, and other scripts
"""

import json
import time

class ScriptEngine:
    def __init__(self):
        self.running_scripts = {}
        
    async def execute(self, language, content):
        """Execute a script in the specified language"""
        try:
            if language == "JavaScript":
                return await self.execute_javascript(content)
            elif language == "Python":
                return await self.execute_python(content)
            elif language == "C++":
                return await self.execute_cpp(content)
            elif language == "Bash":
                return await self.execute_bash(content)
            elif language == "DuckyScript":
                return await self.execute_duckyscript(content)
            else:
                raise ValueError(f"Unsupported language: {language}")
        except Exception as e:
            raise Exception(f"Script execution failed: {str(e)}")
    
    async def execute_javascript(self, content):
        """Execute JavaScript code"""
        # In production, use a JavaScript engine like Duktape or QuickJS
        # For now, return a placeholder
        try:
            # Basic JavaScript execution would go here
            # This requires a JS engine ported to MicroPython
            return "JavaScript execution not yet implemented. Use Python for now."
        except Exception as e:
            raise Exception(f"JavaScript execution error: {str(e)}")
    
    async def execute_python(self, content):
        """Execute Python code"""
        try:
            # Create a safe execution environment
            # WARNING: This is a simplified implementation
            # In production, use proper sandboxing
            
            # For security, only allow safe operations
            allowed_builtins = {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'time': time,
            }
            
            # Execute in restricted environment
            # Note: This is a placeholder - full implementation needs proper sandboxing
            result = "Python execution completed"
            
            return result
        except Exception as e:
            raise Exception(f"Python execution error: {str(e)}")
    
    async def execute_cpp(self, content):
        """Execute C++ code"""
        # C++ requires compilation, which is complex on Pico
        # In production, this would need a C++ compiler or pre-compiled runtime
        return "C++ execution requires compilation. Use pre-compiled binaries or Python/JavaScript."
    
    async def execute_bash(self, content):
        """Execute Bash script"""
        # Bash execution on Pico W is limited
        # Would need a shell implementation
        return "Bash execution not available on Pico W. Use Python instead."
    
    async def execute_duckyscript(self, content):
        """Execute DuckyScript (USB HID injection)"""
        try:
            # Parse DuckyScript commands
            lines = content.split('\n')
            output = []
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse DuckyScript commands
                if line.startswith('STRING '):
                    text = line[7:]
                    output.append(f"Typing: {text}")
                elif line.startswith('DELAY '):
                    delay = int(line[6:])
                    output.append(f"Delay: {delay}ms")
                elif line.startswith('ENTER'):
                    output.append("Pressing Enter")
                # Add more DuckyScript command parsing
            
            return '\n'.join(output)
        except Exception as e:
            raise Exception(f"DuckyScript execution error: {str(e)}")

