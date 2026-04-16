import './metallic-box.css'
import { Box, BoxProps } from "@mui/material"

export default (props:BoxProps) => {
    return (
        <Box className='metallic-box'>
            <Box id='metallic-baby' {...props} sx={{fill:'black', background:'black', ...props.sx}} />
        </Box>
    )
}