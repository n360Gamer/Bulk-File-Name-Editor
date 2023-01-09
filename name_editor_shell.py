
from pathlib import Path
import name_editor


class ShellClient():

    def __init__(self) -> None:
        self.get_folder_location()
        self.editor = name_editor.NameEditor(self.folder)

    def print_files(self) -> None:
        'prints out all the files in the directory'

        print('----------------------------------------------')
        print('|               Found Files                  |')
        print('----------------------------------------------')

        for file in self.editor.get_files():
            print(file)

        print('----------------------------------------------')


    def print_filtered_files(self) -> None:
        'prints all the files from the filtered files list'

        print('----------------------------------------------')
        print('|              Selected Files                |')
        print('----------------------------------------------')
        
        for file in self.editor.get_filtered_files():
            print(file)

        print('----------------------------------------------')


    def get_folder_location(self) -> None:
        'prompts the user for a path to use for finding the folder with all the files'

        self.folder = Path(input('What is the file path for the files: '))

        # checks to see if the path exists and is a folder
        # should probably make these raise an exception later
        try:
            if self.folder.exists() and self.folder.is_dir():
                print('You have opened the folder:', self.folder)

            elif self.folder.is_file():
                print('Please input the directory to a folder, not a file')
                self.get_folder_location()

            else:
                print('Please input a valid directory')
                self.get_folder_location()

        except name_editor.EmptyList:
            print('Please input a directory with files in it')
            self.get_folder_location()

    def get_user_filter_command(self) -> None:
        '''
        this function prompts the user for a command they want to input, it will be the command seperated by a space.
        for example, name test.txt

        if it is not a proper command, it will catch the error IncorrectFilter that is raised 

        also it will keep on looping until the user puts done, that is so the can use multiple filters when selecting files
        '''
        user = ''

        while user != 'done':
            try:
                # uses a strip so if the user puts extra spaces at the end of begining, it wont break it
                user = input('what filters do you want to apply: ').strip()

                if user == 'done':
                    # checks to make sure the filtered list is not empty
                    if len(self.editor.get_filtered_files()) == 0:
                        raise ValueError

                elif user == 'all':
                    cmd = user
                    search = ''
                    # sets the user input to done, since if they select all then theres no more filters to add
                    user = 'done'


                else:
                    cmd, search = user.split(' ')

                self.editor.filter_list(cmd, search)

                self.print_filtered_files()

            except ValueError:
                print('invalid input, please try again')

            except name_editor.IncorrectFilter:
                print('invalid input, please try again')

            except name_editor.EmptyList:
                print(
                    'the filtered list is empty, please use the filter to select the ones to edit')

    def get_file_edit(self) -> None:
        'gets the input from the user on which action they want to do with thier filtered list'

        user = ''

        while user != 'done':
            
            try:
                user = input('which action do you want to do: ')

                if user == 'remove':
                    side = input('which side of the name, (left) or (right): ')
                    amount = int(input('how many characters do you want to remove: '))
                    self.editor.delete_characters_of_file_name(side, amount)

                if user == 'extension':
                    extension = input('what do you want to change the extention to: ')
                    self.editor.rename_file_extension(extension)

            except FileExistsError:
                print('unable to change all files, when the characters are removed, creates files with duplicated names')

            self.print_filtered_files()


test = ShellClient()
test.print_files()
test.get_user_filter_command()
test.get_file_edit()
