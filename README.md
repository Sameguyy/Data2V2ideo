Forked from - https://github.com/Sameguyy/Data2V2ideo

------------------------------------------------------

## Usage
The config.json is used for both decode & encode layout configuration
### * encode
```
$ /encoder /file-to-encode /path-to-output-File
```
### * decode
``Same as encoder``

-------------------------------------------

The main idea was to use WebRTC calls to transmit RTT data, and thus implement some kind of "VPN" functionality based on trusted resources. 

However, I ran into a problem: the two services I wanted to implement this in, which work with whitelists, turned out to have quality 10 times worse than I expected. 

To ensure readability, the frame configuration had to be degraded to monstrously low, "non-working" values, which were not suitable for what I wanted.
