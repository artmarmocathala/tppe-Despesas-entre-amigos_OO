import { createBrowserRouter } from 'react-router-dom';

import { LayoutPrincipal } from './components/LayoutPrincipal';
import { RotaProtegida } from './components/RotaProtegida';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { RecuperarSenha } from './pages/RecuperarSenha';
import { Home } from './pages/Home';
import { ListaGrupos } from './pages/ListaGrupos';
import { Grupo } from './pages/Grupo';
import { Configuracoes } from './pages/Configuracoes';
import { ListaUsuarios } from './pages/ListaUsuarios';

export const router = createBrowserRouter([
  { path: '/login', element: <Login /> },
  { path: '/registrar', element: <Register /> },
  { path: '/recuperar-senha', element: <RecuperarSenha /> },

  {
    path: '/',
    element: <RotaProtegida />,
    children: [{
      element: <LayoutPrincipal />,

      children: [
        {
          index: true,
          element: <Home />,
        },
        {
          path: '/grupos',
          element: <ListaGrupos />,
        },
        {
          path: '/grupos/:id',
          element: <Grupo />,
        },
        {
          path: '/configuracoes',
          element: <Configuracoes />,
        },
        {
          path: '/usuarios',
          element: <ListaUsuarios />,
        }
      ],
    },
  ]},
]);
