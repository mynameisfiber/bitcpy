# About #

BitCpy (Bitly Copy-Paste-y) is a utility that will shorten all urls copied to your clipboard.  In addition, it will provide a fancy notification on systems with pynotify install.

## Installation ##

You must have [xerox](https://github.com/kennethreitz/xerox) and [bitly-api-python](https://github.com/bitly/bitly-api-python) installed for this program to run.

Simply edit the bitcpy.conf file with your [bitly API login credentials](https://bitly.com/a/your_api_key) or copy to ~/.bitcpy.rc.  Install with:

    sudo python ./setup.py install

or

    sudo pip install "https://github.com/mynameisfiber/bitcpy/tarball/master#egg=bitcpy"

## Example setup ##

    #Install dependencies
    pip install xerox
    pip install -e "git://github.com/bitly/bitly-api-python.git#egg=bitly_api"

    #Configuration
    cp bitcpy.conf $HOME/.bitcpyrc
    vim $HOME/.bitcpyrc

    #Install
    python ./setup.py install

    #Run
    bitcpy
