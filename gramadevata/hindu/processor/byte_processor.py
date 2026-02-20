import os

def find_specific_folder(image_location):
    print("venky")
    """
    Function to find a specific folder recursively in the specified search path.
    """
   
    import os
    image_path = os.path.join(r"F:", image_location)

    print(image_path,"ttttttttttttttttttttt")
    if os.path.exists(image_path) and os.path.isdir(image_path):
        # If the folder exists, list all files in it
        images = []
        for root, dirs, files in os.walk(image_path):
            print(root,"llllllllllllllllllllllllllll")
            for file in files:
                images.append(os.path.join(root, file))
                print(files,"iiiiiiiiiiiiiiiiiiiiiii")
        return images
    else:
        # If the folder is not found
        return []


