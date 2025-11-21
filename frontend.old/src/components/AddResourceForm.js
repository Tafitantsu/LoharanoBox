import React, { useState } from 'react';
import axios from 'axios';

const AddResourceForm = ({ fetchResources, setNotification }) => {
    const [name, setName] = useState('');
    const [dockerImageName, setDockerImageName] = useState('');
    const [internalPort, setInternalPort] = useState('');
    const [hostPort, setHostPort] = useState('');
    const [description, setDescription] = useState('');
    const [domain, setDomain] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/resources', {
                name,
                docker_image_name: dockerImageName,
                internal_port: parseInt(internalPort),
                host_port: parseInt(hostPort),
                description,
                domain,
            });
            setNotification({ message: 'Resource added successfully.', type: 'success' });
            fetchResources();
            // Clear form
            setName('');
            setDockerImageName('');
            setInternalPort('');
            setHostPort('');
            setDescription('');
            setDomain('');
        } catch (error) {
            setNotification({ message: 'Failed to add resource.', type: 'error' });
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Add New Resource</h2>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
            <input type="text" value={dockerImageName} onChange={(e) => setDockerImageName(e.target.value)} placeholder="Docker Image" required />
            <input type="number" value={internalPort} onChange={(e) => setInternalPort(e.target.value)} placeholder="Internal Port" required />
            <input type="number" value={hostPort} onChange={(e) => setHostPort(e.target.value)} placeholder="Host Port" required />
            <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" required />
            <input type="text" value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="Domain" required />
            <button type="submit">Add Resource</button>
        </form>
    );
};

export default AddResourceForm;
