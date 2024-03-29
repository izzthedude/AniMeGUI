pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

gnome = import('gnome')

desktop_file = i18n.merge_file(
        input: 'io.github.izzthedude.AniMeGUI.desktop.in',
       output: 'io.github.izzthedude.AniMeGUI.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'io.github.izzthedude.AniMeGUI.appdata.xml.in',
       output: 'io.github.izzthedude.AniMeGUI.appdata.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

install_data('io.github.izzthedude.AniMeGUI.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

gnome.compile_resources('animegui',
  'io.github.izzthedude.AniMeGUI.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

fonts = [
  'NotoColorEmoji.ttf'
]
fontdir = join_paths(pkgdatadir, 'fonts')
install_data(fonts, install_dir: pkgdatadir)

subdir('icons')
