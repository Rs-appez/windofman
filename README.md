# Windofman

A light tool for ordering and switch between multiple dofus windows on linux

![windofman](https://github.com/user-attachments/assets/2327fca9-e038-4a5a-ac7e-51f14629bb58)


## Requirements

- Python 3.8+
- tk (usually installed by default on most Linux distributions)

## Initialization

Setup the virtual environement

```
$ ./init_venv_windofman.sh
```

## Start windofman

```
$ ./windofman.py
```

## Usage

### Link your characeter

Since DOFUS Unity, the window name doesn't take the character name anymore on Linux.  
Therefore, we have to manually link each window with a character.

For each window click on the link button :

![image](https://github.com/user-attachments/assets/16b8e95a-b966-44d8-a0e7-581a7d44ea3f)

- If it is a new character, enter the name and click on **Add new**
  
![create-character](https://github.com/user-attachments/assets/7478c6cd-ef58-4c09-b520-dea79a45c412)

- If the character already exists, click on their name in the list *(you can filter with the input above)*
  
![image](https://github.com/user-attachments/assets/9a75eeee-8035-4e0d-8b06-5d64fd8c0148)

### Features

- Set the initative of each of your characters *(the window will switch on the initiative order)*

- You can clic on your charactere name to directly active the window

- You can ignore a window in the switch loop

### Shortcut
The default shortcuts are :  

- Press **F2** to switch to the next character

- Press **F3** to switch to the previous character  

*You can set your own shortcuts on the shorcuts page*
