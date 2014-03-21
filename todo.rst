To Do
=====

General
-------

* Confirm 0xffff masks are correct

By File
-------

* datatypes
    * computer.py
        * Implement TMATS XML parser
        * Finish formats 2 (recording events)
        * Finish format 3 (index packets)
    * time.py - Add time word parsing
    * ms1553.py - Finish message parsing
    * analog.py - Finish sample parsing (no data to test with)
    * ethernet.py - Implement format 1
    * Implement TSPI/CTS parser

* scripts
    * c10_check.py - Validator
    * c10_reindex.py - Walk a chapter 10 file and build a new index
    * video.py
        * Find what causes the UI hang after load and clean it up
        * Reduce included mplayer and mplayer_pyside dependency footprint
        * Include mplayer binaries for other platforms
        * Allow for immediate playback (while still loading)

* tests - Better coverage for datatypes and top-level package
