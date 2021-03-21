### Web Directory Fuzzer

Web directory fuzzers are important in redteaming. Improper access controls can lead you to places where you are not supposed to be.     
But, you'll have to be aware of such places and there may a fuzzer in handy.    

usage:   
`python3 web_directory_fuzzer.py [-h] [--host HOST] [-r] [-v] path_to_wordlist`      
    `h       -       help`     
    `host    -       host(web URL)(Mandatory)`    
    `r       -       recursive mode(digs deep into directories)`    
    `v       -       verbose`    

It requires a wordlist to get all words from, to bruteforce.
