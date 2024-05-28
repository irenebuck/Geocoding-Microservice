import tkinter as tk
import zmq


def get_coordinates():
    """
    On button click, takes location, makes ZeroMQ socket connection using port 8080, sends address string through socket,
    receives coordinate string, and prints the coordinates to the GUI.
    """
    address = address_entry.get()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:8080")
    socket.send_string(address)
    response = socket.recv_string()

    # Updates the text in the result Label widget with the response value(coordinates)
    result.config(text=response)


# create and size main window
root = tk.Tk()
root.title("Bill's Microservice")
root.geometry('600x200+50+50')

# Create input field for address
user_direction = tk.Label(root, text="Enter Address:")
user_direction.pack(pady=15)
address_entry = tk.Entry(root, width=75, justify='center')
address_entry.pack()

# Create button to submit address and call get_coordinates function
button = tk.Button(root, text="Submit Address", command=get_coordinates)
button.pack(pady=15)

# Create label to display result
result = tk.Label(root, text="")
result.pack()

root.mainloop()