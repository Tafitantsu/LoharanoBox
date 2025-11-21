import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Resource from './Resource';
import AddResourceForm from './AddResourceForm';
import Notifications from './Notifications';

const Dashboard = () => {
    const [resources, setResources] = useState([]);
    const [notification, setNotification] = useState({ message: '', type: '' });

    const fetchResources = async () => {
        try {
            const response = await axios.get('/api/resources');
            setResources(response.data);
        } catch (error) {
            setNotification({ message: 'Failed to fetch resources.', type: 'error' });
        }
    };

    useEffect(() => {
        fetchResources();
        const interval = setInterval(fetchResources, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const handleAction = async (resourceId, action) => {
        try {
            await axios.post(`/api/resources/${resourceId}/${action}`);
            setNotification({ message: `Action ${action} successful for resource ${resourceId}.`, type: 'success' });
            fetchResources();
        } catch (error) {
            setNotification({ message: `Action ${action} failed for resource ${resourceId}.`, type: 'error' });
        }
    };

    return (
        <div>
            <h1>LoharanoBox Dashboard</h1>
            <Notifications notification={notification} />
            <AddResourceForm fetchResources={fetchResources} setNotification={setNotification} />
            <div>
                {resources.map(resource => (
                    <Resource key={resource.id} resource={resource} handleAction={handleAction} />
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
