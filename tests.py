from directories import FileSystem, execute_command, extract_command

test_fs = FileSystem()

assert execute_command(test_fs, extract_command("CREATE fruits")) == "CREATE fruits"
assert test_fs.root == {'fruits': {}}

assert execute_command(test_fs, extract_command("CREATE vegetables")) == "CREATE vegetables"
assert test_fs.root == {'fruits': {}, 'vegetables': {}}

assert execute_command(test_fs, extract_command("CREATE grains")) == "CREATE grains"
assert test_fs.root == {'fruits': {}, 'vegetables': {}, 'grains': {}}

assert execute_command(test_fs, extract_command("CREATE fruits/apples")) == "CREATE fruits/apples"
assert test_fs.root == {'fruits': {'apples': {}}, 'vegetables': {}, 'grains': {}}

assert execute_command(test_fs, extract_command("CREATE fruits/apples/fuji")) == "CREATE fruits/apples/fuji"
assert test_fs.root == {'fruits': {'apples': {'fuji': {}}}, 'vegetables': {}, 'grains': {}}

assert (execute_command(test_fs, extract_command("LIST"))) == "LIST\nfruits\n\tapples\n\t\tfuji\ngrains\nvegetables"

assert execute_command(test_fs, extract_command("CREATE grains/squash")) == "CREATE grains/squash"
assert test_fs.root == {'fruits': {'apples': {'fuji': {}}}, 'vegetables': {}, 'grains': {'squash': {}}}

assert execute_command(test_fs, extract_command("MOVE grains/squash vegetables")) == "MOVE grains/squash vegetables"
assert test_fs.root == {'fruits': {'apples': {'fuji': {}}}, 'vegetables': {'squash': {}}, 'grains': {}}

assert execute_command(test_fs, extract_command("CREATE foods")) == "CREATE foods"
assert test_fs.root == {'fruits': {'apples': {'fuji': {}}}, 'vegetables': {'squash': {}}, 'grains': {}, 'foods': {}}

assert execute_command(test_fs, extract_command("MOVE grains foods")) == "MOVE grains foods"
assert test_fs.root == {'fruits': {'apples': {'fuji': {}}}, 'vegetables': {'squash': {}}, 'foods': {'grains': {}}}

assert execute_command(test_fs, extract_command("MOVE fruits foods")) == "MOVE fruits foods"
assert test_fs.root == {'vegetables': {'squash': {}}, 'foods': {'grains': {}, 'fruits': {'apples': {'fuji': {}}}}}

assert execute_command(test_fs, extract_command("MOVE vegetables foods")) == "MOVE vegetables foods"
assert test_fs.root == {'foods': {'grains': {}, 'fruits': {'apples': {'fuji': {}}}, 'vegetables': {'squash': {}}}}

assert execute_command(test_fs, extract_command("LIST")) == "LIST\nfoods\n\tfruits\n\t\tapples\n\t\t\tfuji\n\tgrains\n\tvegetables\n\t\tsquash"

assert execute_command(test_fs, extract_command("DELETE fruits/apples")) == "DELETE fruits/apples\nCannot delete fruits/apples - fruits does not exist"
assert test_fs.root == {'foods': {'grains': {}, 'fruits': {'apples': {'fuji': {}}}, 'vegetables': {'squash': {}}}}

assert execute_command(test_fs, extract_command("DELETE foods/fruits/apples")) == "DELETE foods/fruits/apples"
assert test_fs.root == {'foods': {'grains': {}, 'fruits': {}, 'vegetables': {'squash': {}}}}

assert execute_command(test_fs, extract_command("LIST")) == "LIST\nfoods\n\tfruits\n\tgrains\n\tvegetables\n\t\tsquash"

assert execute_command(test_fs, extract_command("RENAME fruits")) == "ERROR. Unsupported command:RENAME"

