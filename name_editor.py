from pathlib import Path


class NameEditor():

    def __init__(self, folder) -> None:
        self.files = []
        self.filtered_files = []
        self.folder = folder
        self.search_directory()

    def get_files(self) -> list:
        'returns the files in the given folder'
        return self.files

    def get_filtered_files(self) -> list:
        'returns the files in the given folder'
        return self.filtered_files

    def get_directory(self) -> Path:
        'returns the current directory'
        return self.folder

    def search_directory(self) -> None:
        'searches the folder and makes a list with all the files inside of it'
        # resets it everytime so there is no overlaps between searches, and you dont get duplicates
        self.files = []

        for file in self.folder.iterdir():
            if file.is_file():
                self.files.append(file)

        self._check_if_folder_is_empty()

    def _check_if_folder_is_empty(self) -> None:
        'checks to see if the given directory is empty, and raises the EmptyList exception if it is'

        if len(self.files) == 0:
            raise EmptyList

    def _check_if_filtered_list_is_empty(self) -> None:
        'checks if the filtered list is empty, and raises the EmptyList exception if it is'

        if len(self.filtered_files) == 0:
            raise EmptyList

    def filter_list(self, cmd: str, search: str) -> None:
        '''
        given a command, will filter the current list of files down

        all - selects all files
        name - selects the files that match the exact name
        contains - selects the files with a name that contains a given string of text
        extension - selects the files with a certain extension
        '''

        if cmd == 'all':
            self.filtered_files = self.files

        elif cmd == 'name':
            for file in self.files:
                # you need to add a check to see if the files are already in the list so there are no duplicates when
                # adding multiple filters
                if file.name == search and not (file in self.filtered_files):
                    self.filtered_files.append(file)

        elif cmd == 'contains':
            for file in self.files:
                if search in file.name and not (file in self.filtered_files):
                    self.filtered_files.append(file)

        elif cmd == 'extension':
            for file in self.files:
                if file.suffix == search and not (file in self.filtered_files):
                    self.filtered_files.append(file)

        else:
            raise IncorrectFilter

        self._check_if_filtered_list_is_empty()

    def delete_characters_of_file_name(self, side: str, index: int) -> None:
        '''
        removes the characters from left or right side of the file name given the amount of characters to remove
        for example, given 4, it will remove the 4 characters furtherest to the left, name1234 -> 1234

        the side parameter will indicate which side to remove the characters
        '''

        # this edited list is a temporary list that is used to capture the new path for the edited files
        # so it can update the filtered list
        edited_list = []
        # deletes the characters from the specifed side to the given index
        for file in self.filtered_files:
            if side == 'left':
                new_file = file.rename(file.with_stem(file.stem[index:]))
            elif side == 'right':
                new_file = file.rename(file.with_stem(file.stem[:-index]))

            edited_list.append(new_file)

        self.filtered_files = edited_list

    def rename_file_extension(self, extension : str) -> None:
        '''
        renames the file extension of the selected files
        '''

        # this edited list is a temporary list that is used to capture the new path for the edited files
        # so it can update the filtered list
        edited_list = []
        # deletes the characters from the specifed side to the given index
        for file in self.filtered_files:
            new_file = file.rename(file.with_suffix(extension))
            edited_list.append(new_file)

        self.filtered_files = edited_list


class IncorrectFilter(Exception):
    pass


class EmptyList(Exception):
    pass
