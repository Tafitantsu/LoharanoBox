import React from 'react';

const Resource = ({ resource, handleAction }) => {
    return (
        <div style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
            <h2>{resource.name}</h2>
            <p>{resource.description}</p>
            <p>Status: {resource.status}</p>
            <a href={`http://localhost:${resource.host_port}`} target="_blank" rel="noopener noreferrer">
                Access Resource
            </a>
            <div>
                <button onClick={() => handleAction(resource.id, 'start')}>Start</button>
                <button onClick={() => handleAction(resource.id, 'stop')}>Stop</button>
                <button onClick={() => handleAction(resource.id, 'pull')}>Pull</button>
                <button onClick={() => handleAction(resource.id, 'update')}>Update</button>
            </div>
        </div>
    );
};

export default Resource;
