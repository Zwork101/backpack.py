# backpack.py

This is a library for Backpack.tf's API

## Getting Started 

```
pip install backpack.py
```

### Requirments

 1. Python 3.6
 2. pip (For installation, so optional really)
 3. Internet connection (duh)

## Usage

backpack.py logs into backpack.tf through steam, so you will need your username, password, and shared secret for generating 2fac codes. You can find out how to file your shared secret [here](https://www.google.com/search?q=How+to+file+my+steam+shared+secret). You can also supply your API key for listing searches. For making a listing, you can do this:
```python
from backpackpy import listings

trade_msg = """
Please trade I am but poor man plz thanks  # Don't acually make your details like this
"""

l = listings.Listings('Zwork101', '123456' 'u3iufn847nf') #No, those arn't real
l.create_buy_listing('Genuine', 'Ham Shank', 'tradeoffer_url', 2.66, 0, details=trade_msg)
```

## Authors

* **Zwork101** - *Original Creator* - [My site with links, but is often down, so don't waste your time](https://my-request.tk)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Zwork101/backpack.py/blob/master/MIT_License) file for details

## Acknowledgments

* Backpack.tf!!!!
* People who use this lib
* Works well with the [steam](https://github.com/ValvePython/steam) and [steampy](https://github.com/bukson/steampy) Packages
* Huge thanks to [ShellRox](https://github.com/ShellRox) aka, MrRM, for working with me on logging into backpack.tf through steam!


