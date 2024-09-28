program ifst;	{array}
var ch : array[1000] of array[10] of char;
begin
    readln(ch);
    if ch = 'a' then writeln('It is ''a'' ')
    else writeln('It is not ''a'' ')
end
