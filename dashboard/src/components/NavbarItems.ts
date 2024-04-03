export const NavbarItemsData = [
  {
    title: 'Home',
    description: '',
    url: '/',
  },
  {
    title: 'Graphs',
    description: 'To create, open, import, or export graphs',
    start_path: '/graphs/new',
    color: '#EDF6F9',
    url: '/graphs',
    submenu: [
      {
        title: 'New',
        url: 'new'
      },
      {
        title: 'Open',
        url: 'open'
      },
    ]
  },
  {
    title: 'View',
    description: 'To view the graph in different ways',
    color: '#EDF6F9',
    url: '/view',
    submenu: [
      {
        title: 'Interactive',
        url: 'interactive'
      },
      {
        title: 'Table',
        url: 'table'
      }
    ]
  }
]