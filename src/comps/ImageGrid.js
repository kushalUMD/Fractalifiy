import React from 'react';
const cache = {};

function importAll(r) {
    r.keys().forEach((key) => (cache[key] = r(key)));
}
importAll(require.context("./pngs", false, /\.(png|jpe?g|svg)$/));

const ImageGrid = () => {
    return (
        <div className = "img-grid">
            <h7>
            {Object.entries(cache).map(module => {
            const image = module[1];
            const name = module[0].replace("./","").replace(".png","") + "";
            return (
                <div style={{padding: 10, margin: '0 auto', background: 'white' }}>
                    <img style={{width: 295, margin: '0 auto'}} src= {image} alt = ""/>
                    <p>{name}</p>
                </div>
            )
        })}      
        </h7>  
        </div>
    );
}

export default ImageGrid;