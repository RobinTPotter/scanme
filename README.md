# Flask control for scanimage with pdf stitching

```
gunicorn3 scanmeapp:app --bind=0.0.0.0 --timeout=360 --log-level=debug
```

timeout is important for hi-res scans and stops gunicorn from restarting and
leaving the scanner dangling, required on/off for me

gunicorn's port is 8000, werkzeug is 5000.



may need to add:

```
ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0865", MODE="0666"
```

as a new udev rule in ```/etc/udev/rules.d```




use:

```
sane-find-scanner
```

to find the vendor code




may also need to change a file in:

```
/etc/sane/ ..
```

at the "usb" line.




