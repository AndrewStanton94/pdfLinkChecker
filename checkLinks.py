import ssl
from collections import defaultdict
from pdfx.threadpool import ThreadPool
from pdfx.colorprint import colorprint, OKGREEN, FAIL
from pdfx.downloader import get_status_code

MAX_THREADS_DEFAULT = 7

# Used to allow downloading files even if https certificate doesn't match
if hasattr(ssl, "_create_unverified_context"):
    ssl_unverified_context = ssl._create_unverified_context()
else:
    # Not existing in Python 2.6
    ssl_unverified_context = None


def check_refs(refs, verbose=False, max_threads=MAX_THREADS_DEFAULT):
    """ Check if urls exist """
    codes = defaultdict(list)

    def check_url(ref):
        url = ref.ref
        print(url)
        status_code = str(get_status_code(url))
        codes[status_code].append(ref)
        if verbose:
            if status_code == "200":
                colorprint(OKGREEN, "%s - %s" % (status_code, url))
            else:
                colorprint(FAIL, "%s - %s" % (status_code, url))

    # Start a threadpool and add the check-url tasks
    try:
        pool = ThreadPool(5)
        pool.map(check_url, refs)
        pool.wait_completion()

    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    # Convert URL objects to their URLs
    for code in codes:
        codes[code] = [url.ref for url in codes[code]]
    return codes
