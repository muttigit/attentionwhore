FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/attentionwhore/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/attentionwhore/msg/__init__.py"
  "../src/attentionwhore/msg/_Point.py"
  "../src/attentionwhore/msg/_Trajectory.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
