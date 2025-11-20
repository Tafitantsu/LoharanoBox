import React, { useState, useEffect } from 'react';

const Notifications = ({ notification }) => {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (notification.message) {
            setVisible(true);
            const timer = setTimeout(() => {
                setVisible(false);
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [notification]);

    if (!visible) {
        return null;
    }

    const style = {
        position: 'fixed',
        top: '10px',
        right: '10px',
        padding: '10px',
        backgroundColor: notification.type === 'success' ? 'green' : 'red',
        color: 'white',
        zIndex: 1000,
    };

    return <div style={style}>{notification.message}</div>;
};

export default Notifications;
