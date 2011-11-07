# Installation #

You must have [xerox](https://github.com/kennethreitz/xerox) and [bitly-api-python](https://github.com/bitly/bitly-api-python) installed for this program to run.

Simply edit the bitcpy.conf file with your [bitly API login credentials](https://bitly.com/a/your_api_key) and install with:

    sudo python ./setup.py install

Alternatively, setup file can be copied to $HOME/.bitcpyrc

# Example setup #

    #Install dependencies
    pip install xerox
    pip install -e git://github.com/bitly/bitly-api-python.git#egg=bitly_api

    #Configuration
    cp bitcpy.conf $HOME/.bitcpyrc
    vim $HOME/.bitcpyrc

    #Install
    python ./setup.py install

    #Run
    bitcpy
