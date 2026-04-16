// Component ported and enhanced from https://codepen.io/JuanFuentes/pen/eYEeoyE
import './header.css'
import ASCIIText from '../ascii';
import Box from '@mui/material/Box';
import MetallicBox from '../metallic-box';
export default () => {
    return (
        <Box id='header-box'>
            <MetallicBox  sx={{width:'40vw'}}>
            <ASCIIText
            textColor='white'
                planeBaseHeight={25}
                enableWaves={false}
                textFontSize={32}
                asciiFontSize={5}
                text="Cyberhorse.animus"
            />

                
            </MetallicBox>
        </Box>
    )
}
