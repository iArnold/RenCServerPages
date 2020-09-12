#!/pathto/cgi-bin/renc -c

REBOL [
    title: {Ren-C Web Toolkit.}
    author: {Arnold van Hofwegen, iArnold, Ren-C Open Source Contributors}
    version: 1.0.0.1
    date: 12-9-2020
    rights: {2020 Arnold van Hofwegen}
    license: {Compatible Ren-C license.}
    file: %rencsp.cgi
    other: { This script is loosely based on the rsp.cgi script
             by 2002 Ernie van der Meer, 2003 Maarten Koopmans 
             created for Rebol 2. 
             It has been completely restructured and rewritten
             for use with Ren-C.
           } 
]

result: copy {}

err-to-obj: function [
    {Makes an object! out of an error!}
    err [error!]
    <local> obj
][
    obj: make object! [
        type: _
        id: _
        message: _
        near: _
        where: _
        file: _
        line: _
    ]
    obj/type: err/type
    obj/id: err/id
    obj/message: err/message
    obj/near: err/near
    obj/where: err/where
    obj/file: either err/file [err/file][get-env "PATH_INFO"]
    obj/line: err/line

    obj
]

handle-error: function [o <local> br][
    br: "<br />"
    ;error-message: mold o
    error-message: spaced ["<h3>Error on page</h3>" 
                           "<pre> Type   :" o/type
                           br   "id     :" o/id
                           br   "Message:" o/message
                           br   "Near   :" o/near
                           br   "Where  :" o/where
                           br   "File   :" o/file
                           br   "Line   :" o/line 
                           "</pre>" br
                          ]
    print error-message
]

handle: function [
    {Executes a code block and possible error handling.}
    code [block!] {The code to be evaluated}
    <local> result disarmed ok-or-error
][
    result: copy {}

    ; 'Try' to execute the code.
    ok-or-error: trap code

    if error? ok-or-error [
        handle-error err-to-obj ok-or-error
        return void
    ]

    get/any 'result
]

process-rsp: function [
    {
        Processes a text file. All sections of code between <% and %>
        tags are copied and executed as-is. Code between <%= and %> tags
        is evaluated and replaced by its literal value.
    }
    content [file! text!] {The content to process.}
    <local> code-rule val-rule data code text g-result
][
    ; This would be the place to consult the page cache in case the
    ; argument is a file.
    
    ; 
    code: copy {}
    text: copy {}
    result: copy {}

    code-rule: ["<%" copy data to "%>" thru "%>"]
    val-rule: ["<%=" copy data to "%>" thru "%>"]

    ; Parse input text, constructing a 'compiled' version of the text
    ; in 'code. Things not between "<%" and "%>" will be collected
    ; in a temporary buffer so we don't end up with a zillion append
    ; statements in our compiled page.
    parse either file? content [read content][content][
        any [
            val-rule (
                if not empty? text [
                    append code rejoin [" append result " mold text " "]
                    clear text
                ]
                append code rejoin [" append/only result " data " "]
            ) |
            code-rule (
                if not empty? text [
                    append code rejoin [" append result " mold text " "]
                    clear text
                ]
                append code rejoin [" " data " "]
            ) |
            copy data skip (append text data)
        ]
    ]
    if not empty? text [
        append code rejoin [" append result " mold text " "]
        clear text
    ]

    ; This would be the place to store the code in the page cache.

    ; Execute the constructed code and remember the result.
    code: load code
    do code
    code: load result

    code
]

; Start output, choose 'plain' output for possible debugging
;print "Content-type: text/plain^/^/"
print "Content-type: text/html^/^/"

; Test output can be placed here 

; Continue
handle [
    print process-rsp read/string either system/version/4 <> 3 [
        to-file get-env "PATH_TRANSLATED"
    ][
        ;Handle windows
        to-file join "/" replace/all replace/all
        get-env "PATH_TRANSLATED" "\" "/" ":" ""
   ]
]

; Now output the result, even if an error has been detected
; this will help indicate the spot where the error is occurring.
print result
