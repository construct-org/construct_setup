$this = split-path -parent $MyInvocation.MyCommand.Definition
$old_path = $Env:PATH
$old_python_path = $Env:PYTHONPATH
$Env:PATH = "$this\current\bin;$this\current\python\Scripts;$old_path"
$Env:PYTHONPATH = "$this\current\lib;$old_python_path"

$py_entry_point="$this\current\bin\construct.ps1"
& $py_entry_point @args

$Env:PYTHONPATH=$old_python_path
$Env:PATH=$old_path
Remove-Variable py_entry_point
Remove-Variable old_python_path
Remove-Variable old_path
Remove-Variable this
