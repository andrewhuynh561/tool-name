# n8n Local Docker Setup
# Run this ONCE to start n8n on your computer.
# After this, open http://localhost:5678 in your browser.

docker run -it --rm ^
  --name n8n ^
  -p 5678:5678 ^
  -v "%USERPROFILE%\.n8n:/home/node/.n8n" ^
  -v "C:\Users\andre\Ebay:/data/ebay" ^
  n8nio/n8n
