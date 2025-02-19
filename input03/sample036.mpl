program rcall;
procedure f; begin call g end;
procedure g; begin call f end;
begin call f end.
