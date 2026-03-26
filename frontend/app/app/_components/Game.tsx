'use client'

import { useState } from "react";
import Menu from "./menu/Menu";
import Main from "./main/Main";
import { sendStartGame } from "@/libs/sendStartGame";

export default function Game() {
    const [sessionToken, setSessionToken] = useState<string>();
    const [isLoading, setIsLoading] = useState(false);

    async function onStart() {
        setIsLoading(true);
        const response = await sendStartGame();
        setSessionToken(response.session_token);
        setIsLoading(false);
    }

    if (sessionToken) {
        return <Main sessionToken={sessionToken} />;
    } else {
        return <Menu onStart={onStart} isLoading={isLoading} />;
    }

}