import { useState } from "react";
import Toggle from "./Toggle";
import ActionForm from "./ActionForm";

export interface ActionBarProps {
    sessionToken: string;
}

export default function ActionBar({ sessionToken }: ActionBarProps) {
    const [mode, setMode] = useState<'talk' | 'travel'>('talk');

    const handleTalkClick = () => {
        setMode('talk');
    };

    const handleTravelClick = () => {
        setMode('travel');
    };

    const choices = [
        {
            children: <><i className="fa-regular fa-comment mr-2"></i> Talk</>,
            onClick: handleTalkClick,
            active: mode === 'talk'
        },
        {
            children: <><i className="fa-regular fa-map mr-2"></i> Travel</>,
            onClick: handleTravelClick,
            active: mode === 'travel'
        }
    ]

    return (
        <div className="absolute bottom-0 flex items-center p-4 w-full">
            <Toggle choices={choices} />
            <ActionForm mode={mode} sessionToken={sessionToken} />
        </div>
    );
}
