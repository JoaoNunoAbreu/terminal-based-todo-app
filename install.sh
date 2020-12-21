if [ -n "$ZSH_VERSION" ]; then
   echo "\nalias todo=\"python3 $(pwd)/main.py\"" >> ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
   echo "\nalias todo=\"python3 $(pwd)/main.py\"" >> ~/.bash_profile
fi
