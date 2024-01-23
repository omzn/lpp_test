program sample28p; {call without name}
procedure p;begin writeln('Hello!') end;
procedure q;begin writeln('Everyone!') end;
begin call ; call q end.
