pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'animegui')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'animegui.in',
  output: 'animegui',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

animegui_sources = [
  '__init__.py',
  'app.py',
]

install_subdir('animepy', install_dir: moduledir)
install_subdir('controllers', install_dir: moduledir)
install_subdir('ui', install_dir: moduledir)
install_subdir('utils', install_dir: moduledir)
install_subdir('widgets', install_dir: moduledir)
install_data(animegui_sources, install_dir: moduledir)
