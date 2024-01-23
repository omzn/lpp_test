program error301; {procedure}
procedure p(a:array[10] of integer);begin writeln('Hello!') end;
procedure q;begin writeln('Everyone!') end;
begin call p; call q end.
