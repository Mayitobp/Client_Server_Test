```markdown
# Client-Server String Processor

A client-server application that generates random strings, sends them to a server for processing, and logs the results. The server calculates a "weight" for each string based on specific rules.

## Features
- Generates random strings with letters, digits, and spaces
- TCP communication between client and server
- Weight calculation rules:
  - `1000.00` if contains "aa" (case-insensitive)
  - `(1.5*letters + 2*digits)/spaces` otherwise
  - `INF` if no spaces

## Requirements
- Python 3.x
- No external dependencies needed

## Installation & Usage

1. **Clone/Copy Files**  
Ensure these files are in the same directory:
   ```
   main.py
   client.py
   server.py
   ```

2. **Run the Application**  
```bash
python main.py --host 127.0.0.1 --port 65432 --num-chains 5
```
Replace `5`, `127.0.0.1` and `65432` with desired values, to define host , port and number of chains


3. **Arguments**:
   - `--host`: Server IP (default: 127.0.0.1)
   - `--port`: Communication port (default: 65432)
   - `--num-chains`: Required. Number of strings to generate

## File Structure
```
project/
├── chains.txt            # Generated strings
├── server_responses.txt  # Server's responses
├── client-server.log     # Execution logs
├── main.py               # Main script
├── client.py             # Client logic
└── server.py             # Server logic
```

## Viewing Results

1. **Generated Strings**  
   ```bash
   cat chains.txt
   ```
   Example output:
   ```
   xB7Jk l9jJq3HmZp8C v2RrT...
   ```

2. **Server Responses**  
   ```bash
   cat server_responses.txt
   ```
   Example output:
   ```
   Message received, compute_weight = 22.38
   Message received, compute_weight = 1000.00
   ```

3. **Execution Logs**  
   ```bash
   cat client-server.log
   ```
   Example log entries:
   ```
   2023-10-15 14:30:00,123 - INFO - Generating 5 chains...
   2023-10-15 14:30:01,456 - WARNING - Double 'a' rule detected >> 'AaBc12 3dEf...
   ```

## Code Structure Highlights

### Client Workflow
```python
# Generate 100-character string with 3-5 spaces
def generate_random_string(self):
    length = random.randint(50, 100)
    # ... string generation logic ...
```

### Server Calculation
```python
def get_ponderation(self, chain: str) -> str:
    if any(pair in chain.lower() for pair in ["aa"]):
        return "1000.00"  # Special case
    # Normal calculation
    return f"{(letters*1.5 + numbers*2)/spaces:.2f}"
```

## Notes
- The server handles one connection at a time
- All generated files are overwritten on each execution
- Processing time is logged for performance monitoring
- Use `CTRL+C` to terminate if needed

```
