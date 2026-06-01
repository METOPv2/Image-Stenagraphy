from PIL import Image

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def message_to_binary(message):
    return [format(ord(char), "08b") for char in message]

def encode_data_to_image(image_copy=Image.Image, message=str):
    # add a dot character to the end of message (requried for later deconding)
    message += chr(183)

    # convert the message into the binary
    binary_data = message_to_binary(message)
    binary_data_iter = iter(binary_data)
    binary_data_bits = len(binary_data) * 8

    # general image data
    image_size_x = image_copy.size[0]
    image_size_y = image_copy.size[1]
    total_pixels = image_size_x * image_size_y
    total_channels = total_pixels * 3

    # crucial check
    if binary_data_bits > total_channels:
        raise ValueError("The message is too big for the image.")

    # detailed image data
    pixels = image_copy.get_flattened_data()
    pixels_iter = iter(pixels)

    # states
    pixel = next(pixels_iter)
    pixel_copy = list(pixel)

    channel_position = 0
    (x, y) = 0, 0

    for byte in binary_data:
        for bit in byte:
            channel = int(pixel[channel_position])

            if (is_even(bit) and is_odd(channel)) or (is_odd(bit) and is_even(channel)):
                channel = channel - 1 if channel > 0 else channel + 1

            pixel_copy[channel_position] = channel

            channel_position += 1
            if channel_position == 3:
                image_copy.putpixel((x, y), tuple(pixel_copy))
                channel_position = 0

                pixel = next(pixels_iter)
                pixel_copy = list(pixel)
    
    # returned edited image
    return image_copy

def encode():
    # get the image
    image_name = input("Enter an image name (with extension): ")
    image = Image.open(image_name)

    # get the message
    message = input("Enter a message to hide in the image: ")

    if not message:
        raise ValueError("The message is empty.")
    
    # start encoding the message into the iamge
    image_copy = image.copy()
    encode_data_to_image(image_copy, message)

    # save an image with the encoded message
    new_image_name = input("Enter new image name (with extension). type 'cancel' to cancel the operation: ")
    if new_image_name == "cancel":
        return image_copy.close()
    else:
        image_copy.save(new_image_name, new_image_name.split(".")[-1].upper())

def decode():
    # get the image
    image_name = input("Enter encoded image name (with extension): ")
    encoded_image = Image.open(image_name)

    # general image data
    image_size_x = encoded_image.size[0]
    image_size_y = encoded_image.size[1]
    total_pixels = image_size_x * image_size_y
    total_channels = total_pixels * 3

    # get pixels
    image_pixels = encoded_image.get_flattened_data()
    image_pixels_iter = iter(image_pixels)
    current_pixel = next(image_pixels_iter)
    current_pixel_iter = iter(current_pixel)

    # states
    current_byte = ""
    decoded_message = ""

    step = 0
    while step < total_channels:
        channel = next(current_pixel_iter)
        current_byte += str(int(channel) % 2)

        if (step + 1) % 3 == 0:
            current_pixel = next(image_pixels_iter)
            current_pixel_iter = iter(current_pixel)
        elif (step + 1) % 8 == 0:
            ascii = int(current_byte, 2)
            print(ascii)
            char = chr(ascii)
            decoded_message = decoded_message + char if ascii != 183 else ""
            current_byte = ""

            if ascii == 183:
                break

        step += 1

    print(decoded_message)

    return decoded_message

def main():
    choice = input("Choose operation:\n1. Encode\n2. Decode\n")
    if choice == "1":
        encode()
    elif choice == "2":
        decode()
    else:
        print("Invalid operation")

main()