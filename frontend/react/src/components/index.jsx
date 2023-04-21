import App from './App'
import React from 'react'
import ReactDOM from 'react-dom'
import { StyledEngineProvider } from '@mui/material/styles';


ReactDOM.render(<StyledEngineProvider injectFirst><App />
</StyledEngineProvider>, document.getElementById('root'))
