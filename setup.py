import cx_Freeze

executables = [cx_Freeze.Executable ( "8_puzzle_main.py" )]

cx_Freeze.setup (
   name = "8-puzzle" ,
   options = { "build_exe" : { "packages" : [ "pygame", "pygame_gui" ],
                              "include_files" : ["Roboto-Medium.ttf", "theme.json", "matrix.py", "puzzle_algo.py", "global_colors.py"]}},
   executables = executables
)