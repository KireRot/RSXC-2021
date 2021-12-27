# Day 16 - A scary command

Sometimes while monitoring networks and machines, or doing incident response, we find some obfuscated commands. We didn't have time to deobfuscate this, and it is not recommended to just run it. Could you help us with it?

## Write-Up
So we are given a file with a scary commands.... let's find out what it does. First download the file. If we look closely this looks like shell commands and most of the file are values assigned to variables. The last two lines stands out..

```
x=$(eval "$Hc2$w$c$rQW$d$s$w$b$Hc2$v$xZp$f$w$V9z$rQW$L$U$xZp")
eval "$N0q$x$Hc2$rQW"
```

The *eval* command is the only command that is in clear text at this moment..

From the Internet we can lookup what this command is: "The  eval  utility  shall  construct a command by concatenating arguments together, separating each with a <space>. The constructed command shall be read and executed by the shell."

It will execute things.... So we should not run this script before we know what is does...

We could first *echo* out the value instead of *eval* making the script print out what is wants to do.. Starting with the challenge shell script, we change the last *eval* command to *echo* and run it piping the output to a new file *part2.sh*

This will produce a new script file, very similar to the first one. So we test again... Change *eval* to *echo* and see that it does... Making the script run on our terms...

In the third step we get an other looking script, in more readable form... and er can se that the text is piped to the command *sh* at the end... This we do not want to happen, so we just delete the last part *| sh* and run ...

This giving us yet a similar script as *part4*, which we again delete the last part and run it... and we get this output

```
$ sh part4.sh            
 curl http://rsxc.no/b60b34d2afcd4b3950e4c6341efbc10cdb70e782c70b2bf8950e305ad90ebd5f/flag.txt;#UlNYQ3tEb24ndF9ibGluZGx5X3RydXN0X29iZnVzY2F0ZWRfY29kZV9pdF9taWdodF9kb19zb21ldGhpbmdfYmFkfQ==;#UlNYQ3tEb24ndF9ibGluZGx5X3RydXN0X29iZnVzY2F0ZWRfY29kZV9pdF9taWdodF9kb19zb21ldGhpbmdfYmFkfQ==
```

A *curl* command and to identical strings that looks like *base64*. We can decode these strings and get.

``` shell
$ echo -n UlNYQ3tEb24ndF9ibGluZGx5X3RydXN0X29iZnVzY2F0ZWRfY29kZV9pdF9taWdodF9kb19zb21ldGhpbmdfYmFkfQ== | base64 -d
RSXC{Don't_blindly_trust_obfuscated_code_it_might_do_something_bad}
```

We got our flag!

## The Flag
RSXC{Don't_blindly_trust_obfuscated_code_it_might_do_something_bad}