program undefglobalvar;
procedure f; 
  begin writeln(a) end;
var a : integer;
begin 
  call f 
end.
