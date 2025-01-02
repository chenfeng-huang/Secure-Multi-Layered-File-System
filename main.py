from user_command_io import UserCommandIO

if __name__ == "__main__":
    # Static Test Case
    fs = UserCommandIO()
    '''Make a directory called dir1'''
    print(fs.command_input(["write", "directory", "root/dir1", ""]))

    '''Create a file called file1 with content "Hello World"'''
    print(fs.command_input(["write", "file", "root/dir1/file1", "Hello, World!"]))

    '''Read file1'''
    print(fs.command_input(["read", "file", "root/dir1/file1"]))

    '''Add new content to file1'''
    print(fs.command_input(["write", "file", "/root/dir1/file1", "/+ Another Hello"]))

    '''Read file1'''
    print(fs.command_input(["read", "file", "root/dir1/file1"]))

    '''Make a directory called dir2'''
    print(fs.command_input(["write", "directory", "root/dir2", ""]))

    '''Read root'''
    print(fs.command_input(["read", "directory", "/root"]))

    '''Create a file called file2 inside dir2 with content "File in dir2"'''
    print(fs.command_input(["write", "file", "/root/dir2/file2", "File in dir2"]))

    '''Change access mode of dir2 to read-only'''
    print(fs.command_input(["chmod", "directory", "/root/dir2", "2"]))

    '''Read file2'''
    print(fs.command_input(["read", "file", "root/dir2/file2"]))

    '''Try to delete file2 (should fail due to read-only mode on dir2)'''
    print(fs.command_input(["write", "file", "/root/dir2/file2", "/delete"]))

    '''Change access mode of dir2 to write-only'''
    print(fs.command_input(["chmod", "directory", "/root/dir2", "1"]))

    '''Try to delete file2 (should Success this time)'''
    print(fs.command_input(["write", "file", "/root/dir2/file2", "/delete"]))

    print("------END OF STATIC TEST-------\n\n")
    # Initiate Prompting Test
    fs.run()
    '''---Sample script---'''
    '''Create a directory'''
    # write directory root/dir1 ""


# if __name__ == "__main__":
#     fs = UserCommandIO()

#     # ... (previous test cases)

#     '''Create a directory called dir2'''
#     try:
#         print(fs.command_input(["write", "directory", "/root/dir2", ""]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Create a file called file4 inside dir2 with content "File in dir2"'''
#     try:
#         print(fs.command_input(["write", "file", "/root/dir2/file4", "File in dir2"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Change access mode of dir2 to read-only'''
#     try:
#         print(fs.command_input(["changeMode", "directory", "/root/dir2", "2"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Try to delete file4 (should fail due to read-only mode on dir2)'''
#     try:
#         print(fs.command_input(["write", "file", "/root/dir2/file4", "/delete"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Change access mode of file4 to read-write'''
#     try:
#         print(fs.command_input(["changeMode", "file", "/root/dir2/file4", "3"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Modify content of file4'''
#     try:
#         print(fs.command_input(["write", "file", "/root/dir2/file4", "/+ Modified content"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Read file4'''
#     try:
#         print(fs.command_input(["read", "file", "/root/dir2/file4"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Try to delete file4 again (should still fail due to read-only mode on dir2)'''
#     try:
#         print(fs.command_input(["write", "file", "/root/dir2/file4", "/delete"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Change access mode of dir2 back to read-write'''
#     try:
#         print(fs.command_input(["changeMode", "directory", "/root/dir2", "3"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Delete file4'''
#     try:
#         print(fs.command_input(["write", "file", "/root/dir2/file4", "/delete"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")

#     '''Try to read deleted file4 (should fail)'''
#     try:
#         print(fs.command_input(["read", "file", "/root/dir2/file4"]))
#     except Exception as e:
#         print(f"Error: {str(e)}")