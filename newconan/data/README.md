# {project_name}

# Prerequisite

install `python3`,`git`,`gcc`,`cmake`,`make`,`conan`.

## Ubuntu
```bash
sudo apt install -y git gcc cmake make
#install conan
pip install conan
```

## Windows
Using [scoop](https://scoop.sh/) to install dependencies:
```powershell
# install scoop
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
#install dependencies
scoop install python git gcc cmake
#install conan
pip install conan
```