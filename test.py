import requests

# Original Dropbox shared link
shared_link = "https://www.dropbox.com/scl/fi/dlrfovoroyljqdketdcl9/1403.xlsx?rlkey=rk8p65pggu839rpupq39lz99z&st=cfucybw1&dl=0"

def dropbox_download(link):
    # Modify the link to allow direct access
    direct_link = shared_link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")

    # Use requests to get the content of the file
    response = requests.get(direct_link)

    # Check if the request was successful
    if response.status_code == 200:
        # Specify the local file name where the file will be saved
        local_filename = "downloaded_file.xlsx"  # Replace with your desired file name and extension
        
        # Save the content to a file
        with open(local_filename, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {local_filename}")
    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")

