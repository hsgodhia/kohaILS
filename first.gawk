#!/usr/bin/awk -f

BEGIN       {
            recno = 1;
            title= "-"; author= "-";
            pubdate= "-";
            isbn= "-"; 
            }
/Title/     {
            if(recno > 1)
                {
                print title, ";", author, ";",pubdate, ";",isbn
                }
            recno++;
            subtitle = "-"; author= "-"; edition= "-";
            place= "-"; publisher= "-"; pubdate= "-"; pages= "-";
            isbn= "-"; callno= "-"; accno = "-";
            title = "";
            for(fn = 3; fn <= NF; fn++) title = title " " $fn;
            }

/Publ Dt/ { pubdate = ""; pubdate = $4;} 
/ISBN/ { isbn = ""; isbn = $3;}
/Author/ { author = ""; for( fn = 3; fn <= NF; fn++) author = author " " $fn;}
