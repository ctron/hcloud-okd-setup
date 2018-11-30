# Lessons learned

## NFS recycler broken [OKD 3.10]

This was a problem in OKD 3.10. The NFS recycler was broken. There was a
workaround for this:

    echo "OPENSHIFT_RECYCLER_IMAGE=openshift/origin-recycler:v3.10.0" >> /etc/origin/master/master.env

**Note:** This seems to be no longer necessary for OKD 3.11 and so it is
          dropped from the scripts.
