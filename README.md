# WFW

CLI for WorkFlowy inspired by [WWW::Workflowy](https://github.com/cotto/www-workflowy).

WorkFlowy does not maintain an external API, so the cli can break anytime. Do not use it for anything mission critical.

##Commands

#### wfw export <filename>

Export the list to file. The output file can be imported to hnb.

filename: path to file, default: tree.exported in current directory

`wfw export`

`wfw export my-pretty-file`

####  wfw fetch

Fetch list from WorkFlowy server. Prompts for e-mail and password.

email: registered e-mail  
password: password

`wfw fetch`

#### wfw show --root <root> <depth>

Prints list until given depth.

root: text of the root item, default: root of tree  
depth: height of tree to be printed, default: 1

`wfw show`

`wfw show 2`

`wfw show --root personal 3`

#### wfw tag <tag-to-find>

Find items containing the given tag.

tag-to-find: name of tag to find

`wfw tag @work`

`wfw tag "#ThisWeek"`

## TODO

* note handling
* bold, italic text
* show if item completed
* add item
* remove item

## Author

Noemi Vanyi <sitbackandwait@gmail.com\>
