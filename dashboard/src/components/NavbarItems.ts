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
    title: 'Run',
    description: 'To run a process over a selected graph, for example search',
    url: '/run',
    start_path: '/run/search',
    color: '#EDF6F9',
    submenu: [
      {
        title: 'Search',
        url: 'search'
      },
      {
        title: 'Process 2',
        url: 'process-2'
      }
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