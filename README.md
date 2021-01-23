# [devnotes](https://github.com/devon-badman/devnotes)
A simple notes plugin for SublimeText

Use:
- Super+F4 to create a new note
    - creating a note with a title like "folder/subfolder/title" will store the note inside those folders, inside your normal note location.

- Super+Shift+F4 to create a new linked note.
    - This will create a [[link]] to your note at your current cursor locations.

- Super+Shift+F1 to follow a link
    - This will open the notes are your current cursor locations. If the note does not exist, it will be created.

Settings:
- in your user settings or project settings you can set the following options
```json
{
    "root": "~/devnotes/Notes/",
    "note_save_extension": "md"
}
```

## License

Copyright 2021 [Devon Badman](https://github.com/devon-badman).
Licensed under the MIT License

## Acknowledgments

Thanks to the creators of the following plugins for inspiration and code snippets.
- https://github.com/aziz/PlainNotes
- https://github.com/aronwoost/sublime-expand-region