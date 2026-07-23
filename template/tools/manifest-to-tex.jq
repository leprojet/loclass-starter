def tex:
  tostring
  | gsub("\\\\"; "\u001e")
  | gsub("\\{"; "\\{")
  | gsub("\\}"; "\\}")
  | gsub("#"; "\\#")
  | gsub("\\$"; "\\$")
  | gsub("%"; "\\%")
  | gsub("&"; "\\&")
  | gsub("_"; "\\_")
  | gsub("\\^"; "\\textasciicircum{}")
  | gsub("~"; "\\textasciitilde{}")
  | gsub("\u001e"; "\\textbackslash{}");

def root:
  if (.manifest? | type) == "object"
  then .manifest
  else .
  end;

def metadata:
  (root) as $root
  | if ($root.metadata? | type) == "object"
    then $root.metadata
    else $root
    end;

metadata as $m
| [
    "\\title{" + (($m.title // "Neues loclass-Dokument") | tex) + "}",
    "\\subtitle{" + (($m.subtitle // "") | tex) + "}",
    "\\author{" + (($m.author // "") | tex) + "}",
    "\\Company{" + (($m.company // "") | tex) + "}",
    "\\Customer{" + (($m.customer // "") | tex) + "}",
    "\\Version{" + (($m.version // "") | tex) + "}",
    (
      if (($m.date // "") | tostring) == ""
      then "\\date{\\today}"
      else "\\date{" + ($m.date | tex) + "}"
      end
    )
  ]
| .[]
