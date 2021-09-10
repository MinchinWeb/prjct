import invoke

#import minchin.releaser
try:
    from minchin.releaser import make_release, vendorize
except ImportError:
    print("[WARN] minchin.releaser not installed")
