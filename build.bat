pyinstaller -F kindo/__main__.py --clean -i kindo/app.ico -n kindo.exe --distpath=bin && rd /s /q build && del /q /s kindo.exe.spec
